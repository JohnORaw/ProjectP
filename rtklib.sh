# Install prereqs
sudo apt install cmake -y
sudo apt install libev-dev -y 
sudo apt install git -y

# Get RTKLIB
git clone https://github.com/tomojitakasu/RTKLIB.git -b rtklib_2.4.3

# Compile str2str
cd RTKLIB/app/consapp/str2str/gcc
make

# Copy str2str up to home directory
cp str2str ~/
cd ~
