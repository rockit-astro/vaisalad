rpm:
	python3 setup.py bdist_rpm

clean:
	python3 setup.py clean
	rm -rf build dist
