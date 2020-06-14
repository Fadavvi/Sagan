RED='\033[0;31m'
NC='\033[0m'
echo -e ${RED}' ==============================\n'
echo -e '|  Sagan Installtion Script    |\n'
echo -e '|            V0.1              |\n'
echo -e '|      by Milad Fadavvi        |\n'
echo -e '|     Run Script as ROOT       |\n'
echo -e ' ==============================\n\n'
echo  -e 'Step 1 : install Available Packages\n'
yum groupinstall -y 'Development Tools'
yum install -y git wget libtool libyaml-devel net-snmp net-snmp-perl snmptt  perl-Sys-Syslog \
                    libesmtp-devel libpcap-devel pcre-devel geoip-devel gnutls-devel prelude-devel \
                    daq-devel glibc-static libestr-devel libfastjson-devel liblognorm-devel flex flow-tools \
                    rrdtool-devel rrdtool-perl flex flow-tools rrdtool-devel rrdtool-perl  byacc bison
                    
echo -e ${RED}'\n\nStep 2: Install GeoIP Lib & Database\n'${NC}
mkdir /usr/local/share/GeoIP
wget http://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.tar.gz
tar xvzf GeoLite2-Country.tar.gz
cd GeoLite2-Country*
mv GeoLite2-Country.mmdb /usr/local/share/GeoIP/
git clone --recursive https://github.com/maxmind/libmaxminddb
cd libmaxminddb
./bootstrap
./configure
make check
make install
ldconfig
cd ..
echo -e ${RED}'\n\nStep 2.5!: Hredis installation\n'${NC}
git clone https://github.com/redis/hiredis.git
cd hiredis
make && make install
ln -s /usr/local/lib/libhiredis.so.0.14 /usr/local/lib64/libhiredis.so.0.14
LD_LIBRARY_PATH=/usr/local/lib64
export LD_LIBRARY_PATH
ldconfig
cd ..
echo -e ${RED}'\n\nStep 3: install libfastjson \n'${NC}
git clone https://github.com/rsyslog/libfastjson
cd libfastjson
./autogen.sh
./configure --libdir=/usr/lib --includedir=/usr/include
make && make install
ldconfig
cd ..
echo -e ${RED}'\n\nStep 4: install libestr \n'${NC}
git clone https://github.com/rsyslog/libestr
cd libestr/
autoreconf -vfi
./configure --libdir=/usr/lib --includedir=/usr/include
make && make install
ldconfig
cd ..
echo -e ${RED}'\n\nStep 5: install  liblognorm\n'${NC}
git clone https://github.com/rsyslog/liblognorm
cd liblognorm/
autoreconf -vfi
./configure --disable-docs --libdir=/usr/lib --includedir=/usr/include  --enable-regexp --enable-advanced-stats --enable-valgrind
make && make install
ldconfig
cd ..
echo -e ${RED}'\n\nStep 6: install libdnet\n'${NC}
git clone https://github.com/jncornett/libdnet
cd libdnet/
./configure && make && make install
ldconfig
cd ..
echo -e ${RED}'\n\nStep 7: install  Sagan\n'${NC}
git clone https://github.com/beave/sagan
cd sagan/
./autogen.sh
./configure --enable-geoip --enable-esmtp --enable-libpcap --enable-redis --enable-dependency-tracking
make && make install
ldconfig
cd .. 
echo -e ${RED}'\n\nStep 8: Install Barnyard2 for Sagan\n'${NC}
git clone https://github.com/firnsy/barnyard2
cd barnyard2*
./autogen.sh 
./configure --enable-prelude LIBS="-pthread"
make && make install
ldconfig
cd ..
echo -e ${RED}'\n\nStep 9: Install Netflow Support\n'${NC}
git clone https://github.com/beave/nfdump-1.6.10p1-sagan
cd nfdump-1.6.10p1-sagan
./configure --enable-sflow --enable-nfprofile --enable-nftrack --enable-sagan --enable-nsel
make && make install
ldconfig
echo -e ${RED}'\n\nStep 10: Install SNMPTrap Support\n'${NC}
echo 'OPTIONS="-On -Lsd -p /var/run/snmptrapd.pid"' >> /etc/sysconfig/snmptrapd
echo 'traphandle default /usr/sbin/snmptthandler' >> /etc/snmp/snmptrapd.conf
echo 'disableAuthorization yes' >> /etc/snmp/snmptrapd.conf
service snmptrapd start
chkconfig snmptrapd on
service snmptt start
chkconfig snmptt on
sh -c "echo /usr/local/lib  >> /etc/ld.so.conf.d/local.conf"
$ ldconfig
echo ${RED}'\n\nStep 11: download Sagan Rules\n'${NC}
cd /usr/local/etc
git clone https://github.com/beave/sagan-rules
echo -e ${RED}'\n\nStep 12: Add Sagan user\n'${NC}
adduser sagan --disabled-password --disabled-login
mkdir /var/log/sagan
mkdir /var/run/sagan
mkdir /var/sagan/
mkdir /var/sagan/ipc
mkdir /var/sagan/fifo/
mkdir /var/log/sagan/stats
touch /var/log/sagan/stats/sagan.stats
chown -R sagan /var/sagan
chown -R sagan /var/run/sagan
chown -R sagan /var/sagan
chown -R sagan /var/log/
mkfifo /var/sagan/fifo/sagan.fifo
echo -e ${RED}'Notice!! you should change : \n'
echo -e '/usr/local/etc/sagan.yaml \n\n'
echo -e 'GeoIP file: /usr/local/share/GeoIP/GeoLite2-City.mmdb \n'
echo -e 'SNMP conf : /etc/snmp/snmptt.ini '
echo -e 'Netflow Tool: /usr/local/bin/nfcapd '
echo -e 'Rules are stored in: /usr/local/etc/sagan-rules'${NC}
sh -c "echo /usr/local/lib  >> /etc/ld.so.conf.d/local.conf"
 ldconfig
