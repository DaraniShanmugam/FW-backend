# FW-backend
JSON-Merge

main.py is the file which has all fuctionalities for merging json files,
  - command line to execute the file is "python main.py <folderpath> --inprefix <input file base name> output --outprefix <output file base     name> --max <maximum size of file> <key>", as told it accepts all input paramaters
  - the file contains two function, named as main() and merge()
  -main()
   => this function gets the input parameters from the user.
   => read all files in the Folder Path that begin with the Input File Base Name, and process them in increasing order of the number added       as a suffix to each file
   => the file is sent to merge function in increasing order for processing further
  -merge()
   => ensures the input file exists
   => ensures output directory exists or create new
   => gets the base size of json data
   => checks whether the file is json file
   => check the key is present in json file
   => check the output file has any items previously, if not add directly, else, add comma and space with the item
   => If item is too large, it cannot be store in any file. That particular record will be skipped
   => If output_size and item_size is greater than maximum file size then new file is created and item is stored
   => It supports non-english characters
  
  -Complexity of algorithm,
    O(n), where n is the total number of items in a combined array
    
  -Language used is Python
  -Unit testing is done to test the number of files in output file and each output file size is equal or not.
  
    
