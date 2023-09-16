# Instructions to create requests for SUS samples

### Check list
    - `container.py` : Update the file with your requirements like fragments, gridpacks, number of events 
    - `create_requests.py` : Create a csv file from the provided infomation from container.py 
    - `getCookie.sh` : create the MccM utility environment
    - `manageRequests.py` : create requests in MccM
    - Create a toy PrepID in MccM page by clonning the campaigns (2016, 2016APV, 2017, 2018), later can be deleted. This toy will be the framework for the new requests. The filter efficicency will be updated from this Toy PrepID     

### Commands to follow up
     - `python create_requests.py`
     - `source getCookie.sh`
     - `python manageRequests.py <csv_file> --clone <Toy_PrepID> `
     - by the --dry option, you can test the script without submitting it to MccM page