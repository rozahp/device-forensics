## Make backup of device

### 1. Check connection with device

ideviceinfo

### 2. Enable password

idevicebackup2 -i encryption on

### 3. Make backup

idevicebackup2 backup --full /path/to/backup

### 4. Exctract backup key 

mvt-ios extract-key -k backup.key /path/to/backup

### 5. Decrypt backup

mvt-ios decrypt-backup -k backup.key -d /path/to/decryption /path/to/backup

### 6. Check Backup

mvt-ios check-backup --output /path/to/output /path/to/decryption

### 7. Download iocs

mvt-ios download-ios

### 8. Check iocs against output 

mvt-ios check-iocs --iocs /path/to/malware.stix2 /path/to/output

### EOF
