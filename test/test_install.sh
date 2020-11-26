rm -rf res
mkdir res
cd res || exit

rm -rf dfn
mkdir dfn
cd dfn || exit
wget https://github.com/cltl/DutchFrameNet/archive/v0.1.zip
unzip v0.1.zip
cd ../..