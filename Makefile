mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
curr_dir := $(patsubst %/,%,$(dir $(mkfile_path)))

include Makefile.vars

onos_url := http://localhost:8181/onos
onos_curl := curl --fail -sSL --user onos:rocks --noproxy localhost
app_name := org.onosproject.ngsdn-tutorial

NGSDN_TUTORIAL_SUDO ?=

default:
	$(error Please specify a make target (see README.md))

_docker_pull_all:
	docker pull ${ONOS_IMG}@${ONOS_SHA}
	docker tag ${ONOS_IMG}@${ONOS_SHA} ${ONOS_IMG}
	docker pull ${P4RT_SH_IMG}@${P4RT_SH_SHA}
	docker tag ${P4RT_SH_IMG}@${P4RT_SH_SHA} ${P4RT_SH_IMG}
	docker pull ${P4C_IMG}@${P4C_SHA}
	docker tag ${P4C_IMG}@${P4C_SHA} ${P4C_IMG}
	docker pull ${STRATUM_BMV2_IMG}@${STRATUM_BMV2_SHA}
	docker tag ${STRATUM_BMV2_IMG}@${STRATUM_BMV2_SHA} ${STRATUM_BMV2_IMG}
	docker pull ${MVN_IMG}@${MVN_SHA}
	docker tag ${MVN_IMG}@${MVN_SHA} ${MVN_IMG}
	docker pull ${GNMI_CLI_IMG}@${GNMI_CLI_SHA}
	docker tag ${GNMI_CLI_IMG}@${GNMI_CLI_SHA} ${GNMI_CLI_IMG}
	docker pull ${YANG_IMG}@${YANG_SHA}
	docker tag ${YANG_IMG}@${YANG_SHA} ${YANG_IMG}
	docker pull ${SSHPASS_IMG}@${SSHPASS_SHA}
	docker tag ${SSHPASS_IMG}@${SSHPASS_SHA} ${SSHPASS_IMG}

deps: _docker_pull_all

_start:
	$(info *** Starting ONOS and Mininet (${NGSDN_TOPO_PY})... )
	@mkdir -p tmp/onos
	@NGSDN_TOPO_PY=${NGSDN_TOPO_PY} docker-compose up -d

start: NGSDN_TOPO_PY := topo.py
start: _start

stop:
	$(info *** Stopping ONOS and Mininet...)
	@NGSDN_TOPO_PY=foo docker-compose down -t0

restart: reset start

onos-cli:
	$(info *** Connecting to the ONOS CLI... password: rocks)
	$(info *** Top exit press Ctrl-D)
	@ssh -o "UserKnownHostsFile=/dev/null" -o "StrictHostKeyChecking=no" -o LogLevel=ERROR -p 8101 onos@localhost

onos-log:
	docker-compose logs -f onos

onos-ui:
	open ${onos_url}/ui

mn-cli:
	$(info *** Attaching to Mininet CLI...)
	$(info *** To detach press Ctrl-D (Mininet will keep running))
	-@docker attach --detach-keys "ctrl-d" $(shell docker-compose ps -q mininet) || echo "*** Detached from Mininet CLI"

mn-log:
	docker logs -f mininet

_netcfg:
	$(info *** Pushing ${NGSDN_NETCFG_JSON} to ONOS...)
	${onos_curl} -X POST -H 'Content-Type:application/json' \
		${onos_url}/v1/network/configuration -d@./mininet/${NGSDN_NETCFG_JSON}
	@echo

netcfg: NGSDN_NETCFG_JSON := netcfg.json
netcfg: _netcfg

_copy_p4c_out:
	$(info *** Copying p4c outputs to app resources...)
	@mkdir -p app/src/main/resources
	cp -f p4src/build/p4info.txt app/src/main/resources/
	cp -f p4src/build/bmv2.json app/src/main/resources/

_mvn_package:
	$(info *** Building ONOS app...)
	@mkdir -p app/target
	@docker run --rm -v ${curr_dir}/app:/mvn-src -w /mvn-src ${MVN_IMG} mvn -o clean package

app-build: p4-build _copy_p4c_out _mvn_package
	$(info *** ONOS app .oar package created succesfully)
	@ls -1 app/target/*.oar

app-install:
	$(info *** Installing and activating app in ONOS...)
	${onos_curl} -X POST -HContent-Type:application/octet-stream \
		'${onos_url}/v1/applications?activate=true' \
		--data-binary @app/target/ngsdn-tutorial-1.0-SNAPSHOT.oar
	@echo

app-uninstall:
	$(info *** Uninstalling app from ONOS (if present)...)
	-${onos_curl} -X DELETE ${onos_url}/v1/applications/${app_name}
	@echo

app-reload: app-uninstall app-install



install:
	source /etc/lsb-release
	echo "deb http://download.opensuse.org/repositories/home:/p4lang/xUbuntu_${DISTRIB_RELEASE}/ /" | sudo tee /etc/apt/sources.list.d/home:p4lang.list
	curl -fsSL https://download.opensuse.org/repositories/home:p4lang/xUbuntu_${DISTRIB_RELEASE}/Release.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/home_p4lang.gpg > /dev/null
	sudo apt-get update
	sudo apt install p4lang-p4c
	pip3  install grpcio grpcio-tools

p4-build: p4src/main.p4
	$(info *** Building P4 program...)
	@mkdir -p p4src/build
	docker run --rm -v ${curr_dir}:/workdir -w /workdir ${P4C_IMG} \
		p4c-bm2-ss --arch v1model -o p4src/build/bmv2.json \
		--p4runtime-files p4src/build/p4info.txt --Wdisable=unsupported \
		p4src/main.p4
	@echo "*** P4 program compiled successfully! Output files are in p4src/build"

build-proto: 
	python3 -m grpc_tools.protoc --proto_path=proto proto/p4/v1/p4data.proto proto/p4/config/v1/p4info.proto proto/p4/config/v1/p4types.proto proto/google/rpc/status.proto proto/google/rpc/code.proto proto/p4/tmp/p4config.proto proto/p4/server/v1/config.proto proto/p4/v1/p4runtime.proto --python_out=. --grpc_python_out=.
