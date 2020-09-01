# Sagan


<cite>[Sagan git : (https://github.com/beave/sagan) ]</cite>

    sagan_install_centos_fedora.sh
    
    Install Sagan on CentOS/Fedora (with all needed libs and barnyard2 & downloading Rules)
    
 -------------------------------------------
    
     Sagan_Auto_start.sh + sagan.service
	
    Resolve /var/run/sagan/ problem for each start & auto start.
    
-------------------------------------------
    
    MISP (https://github.com/MISP/MISP) Integration
    
    Python script than enable Sagan to save and use MISP Bro Int (Zeek Int) or Snort Rules. (Just Cron it!)
    ** Known issue: Snort rule file size cause of Sagan failed to start. Be careful.
    
-------------------------------------------

    Rule Parser: (python3 + MongoDB)
    * pymongo Library is required (pip3 install pymongo | python3 -m pip install pymongo)
    ** change IP, Port, Username and password on MongoDB host in "cfg" file
    
    Parse Sagan rules and insert into the MongoDB
  	-h, --help            show help message and exit
  	--path PATH           Path of rules [Required]
  	--enabled             add enabled tag to parsed rules
  	--default DEFAULT     add default tag to parsed rules (1,2,3)
  	--autoxbit            add (auto generated) XBIT SET name to parsed rules
  	--userdef USERDEFName USERDEFValue	 add user defined (single) tag to parsed rules
    
    Sample usage:
    python3 Sagan-Rule-Parser.py --path ok-rules/ --autoxbit --default 1 --enabled
    
    
    MongoDB installation guide: (https://docs.mongodb.com/manual/administration/install-community/)
    Secure MongoDB with (https://www.psychz.net/client/question/en/how-to-secure-mongodb-on-centos-7.html)
    
