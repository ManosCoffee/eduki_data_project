### Prerequisites 
- Have Docker installed, preferably in MacOS or linux.

### Instructions 
 
 1. ‘git clone‘ in your local folder from :
 https://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@github.com/ManosCoffee/eduki_data_project.git 

2. Instead of having headaches ...just use my Makefile: 
    - run ‘make build’ to build the image (this could take a while the first time - maybe more than 5 minutes)
    - run ‘make up’ to initialize  the network of the ‘eduki_image’ and the local ‘Postgres db’ that I have set up for this case
     -run ‘make run MODULE_NAME="<module_name>"’ to run the desired ingestion operation!  

     
    👉MODULE_NAME=”bigquery_ingestion_operator” for  BQ 
    👉MODULE_NAME=”postgresql_ingestion_operator” for Postgres