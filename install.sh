rm -rf res
mkdir res
cd res || exit
git clone https://github.com/cltl/multilingual-wiki-event-pipeline || exit

rm -rf dfn
mkdir dfn
cd dfn || exit
wget https://github.com/cltl/DutchFrameNet/archive/v0.1.zip || exit
unzip v0.1.zip
cd ../..

cd src || exit
rm -rf LexicalDataD2TAnnotationTool
git clone https://github.com/cltl/LexicalDataD2TAnnotationTool || exit
cd LexicalDataD2TAnnotationTool || exit
pip install -r requirements.txt
#bash install.sh
cd ../..

cd src || exit
rm -rf FrameNetNLTK
git clone https://github.com/cltl/FrameNetNLTK || exit
cd FrameNetNLTK || exit
pip install -r requirements.txt
bash install.sh
cd ..

rm -rf historical_distance || exit
git clone https://github.com/cltl/historical_distance || exit





