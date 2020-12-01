rm -rf res
mkdir res
cd res || exit
git clone https://github.com/cltl/multilingual-wiki-event-pipeline

rm -rf dfn
mkdir dfn
cd dfn || exit
wget https://github.com/cltl/DutchFrameNet/archive/v0.1.zip
unzip v0.1.zip
cd ../..

cd src || exit
rm -rf LexicalDataD2TAnnotationTool
git clone https://github.com/cltl/LexicalDataD2TAnnotationTool
cd LexicalDataD2TAnnotationTool || exit
pip install -r requirements.txt
bash install.sh
cd ../..

cd src || exit
git clone https://github.com/cltl/FrameNetNLTK
cd FrameNetNLTK || exit
pip install -r requirements.txt
bash install.sh
cd ..

git clone https://github.com/cltl/historical_distance





