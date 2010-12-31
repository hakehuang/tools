#!/bin/sh

name=ltp-imx

read -p "will clone from git master to generate release tar balls. press to continue"

vte_version=101200

read -p "please define the vte release version:" vte_version


git clone b20222@10.192.225.222:/home/git-repository/vte

git checkout master

cd vte

git checkout -b REL_${vte_version}

echo "moves out the test data first"
mv testcases/vte_tests_suite/test_data ../

tar czvf ../${name}_0001_vte_source_${vte_version}.tar.gz testcases/vte_tests_suite
tar czvf ../${name}_0002_open_module_test_${vte_version}.tar.gz testcases/module_test/open_source_module
tar czvf ../${name}_0003_vte_module_test_${vte_version}.tar.gz testcases/module_test/vte_test_modules
echo "move in test data"
mv ../test_data testcases/vte_tests_suite/
tar czvf ../${name}_0004_vte_test_data_${vte_version}.tar.gz testcases/vte_tests_suite/test_data
tar czvf ../${name}_0005_add_module_test_${vte_version}.tar.gz testcases/module_test/Makefile
tar czvf ../${name}_0006_add_top_makefile_${vte_version}.tar.gz Makefile_vte
tar czvf ../${name}_0007_add_armconfig_${vte_version}.tar.gz armconfig package_manifest.txt EULA

