RPMBUILD = rpmbuild --define "_topdir %(pwd)/build" \
        --define "_builddir %{_topdir}" \
        --define "_rpmdir %{_topdir}" \
        --define "_srcrpmdir %{_topdir}" \
        --define "_sourcedir %(pwd)"

GIT_VERSION = $(shell git name-rev --name-only --tags --no-undefined HEAD 2>/dev/null || echo git-`git rev-parse --short HEAD`)
SERVER_VERSION=$(shell awk '/Version:/ { print $$2; }' vaisala-server.spec)

all:
	mkdir -p build
	cp vaisalad vaisalad.bak
	awk '{sub("SOFTWARE_VERSION = .*$$","SOFTWARE_VERSION = \"$(SERVER_VERSION) ($(GIT_VERSION))\""); print $0}' vaisalad.bak > vaisalad
	${RPMBUILD} -ba vaisala-server.spec
	${RPMBUILD} -ba vaisala-client.spec

	cp vaisalad-test vaisalad-test.bak
	awk '{sub("SOFTWARE_VERSION = .*$$","SOFTWARE_VERSION = \"$(SERVER_VERSION) ($(GIT_VERSION))\""); print $0}' vaisalad-test.bak > vaisalad-test
	cp vaisala vaisala.bak
	awk '{sub("PYRO_HOST = .*$$","PYRO_HOST = \"localhost\""); print $0}' vaisala.bak > vaisala

	${RPMBUILD} -ba vaisala-test.spec
	mv build/noarch/*.rpm .
	rm -rf build
	mv vaisalad.bak vaisalad
	mv vaisala.bak vaisala
	mv vaisalad-test.bak vaisalad-test

