from django.shortcuts import render
import pandas as pd
import os,io
import csv
from django.contrib import messages
from pathlib import Path
import requests

#### Create Function 


#### Create your views here.

#Home View
def Home_View(request) :
    
    return render(request,'base.html',{})

# Upload and process data view
def upload_csv(request):

    if request.method == "POST" :
        #Check if file is selected
        if len(request.FILES) != 0:


            myfile = request.FILES['data_file']
            
            # List Of All Required Files
            files = ('csv','xlsx')

            # check if it's csv file :
            if not myfile.name.endswith(files) :

              #Produce Warning Message  
              messages.add_message(request,messages.WARNING, 'Please Upload a CSV or XLSX File!!!') 
              return render(request,'base.html')

            
        
            else : 
                # Read csv file InMemoryUploadedFile
                file = myfile.read().decode('utf-8')
                reader = csv.DictReader(io.StringIO(file))


                # Generate a DataFrame comprehension
                data = pd.DataFrame([line for line in reader]).to_dict('records')

                # Json file to request Transformer
                JSON_FILE={
                    "entities": data ,
                    "globalTransformers": [
                        
                        {
                            "name": "normalize",
                            "order": "before"
                        },

                    ],    "attributeTransformers": []
    
                    
                }
                try :
                    # Request Transformer and get results
                    r = requests.post("http://localhost:8080", json=JSON_FILE)
                    
                    ### Download Results
                    # Transform from json to dataframe
                    Data_Processed = pd.DataFrame(r.json()['entities'])

                    # Get path to Downloads folder
                    path_to_download_folder = str(os.path.join(Path.home(), "Downloads")) +"\Processed_"+ myfile.name    

                    # Download Data     
                    Data_Processed.to_csv(path_to_download_folder,index=False)
                    
                    # Produce Success Message         
                    messages.add_message(request,messages.SUCCESS, 'Success Processing. Please Check Downloads...') 
                    
                    return render( request, 'base.html')

                except :
                    
                    # Produce Success Message         
                    messages.add_message(request,messages.WARNING, 'Please refresh the page and try again...') 
                    return render( request, 'base.html')


                        
                
                
                return render(request,'base.html')
                

        else :
           # Submit Without choosing afile 
           messages.add_message(request,messages.WARNING, 'Please Choose a File!!!') 
           return render( request, 'base.html')    