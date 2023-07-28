RPMBUILD = rpmbuild --define "_topdir %(pwd)/build" \
        --define "_builddir %{_topdir}" \
        --define "_rpmdir %{_topdir}" \
        --define "_srcrpmdir %{_topdir}" \
        --define "_sourcedir %(pwd)"

all:
	mkdir -p build
	date --utc +%Y%m%d%H%M%S > VERSION
	${RPMBUILD} --define "_version %(cat VERSION)" -ba rockit-vaisala.spec
	${RPMBUILD} --define "_version %(cat VERSION)" -ba python3-rockit-vaisala.spec

	mv build/noarch/*.rpm .
	rm -rf build VERSION

install:
	@date --utc +%Y%m%d%H%M%S > VERSION
	@python3 -m build --outdir .
	@sudo pip3 install rockit.vaisala-$$(cat VERSION)-py3-none-any.whl
	@rm VERSION
	@cp vaisalad vaisala /bin/
	@cp vaisalad@.service /usr/lib/systemd/system/
	@cp completion/vaisala /etc/bash_completion.d/
	@install -d /etc/vaisalad
	@echo ""
	@echo "Installed server, client, and service files."
	@echo "Now copy the relevant json config files to /etc/vaisalad/"
	@echo "and udev rules to /usr/lib/udev/rules.d/"
