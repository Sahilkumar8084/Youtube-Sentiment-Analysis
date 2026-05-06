1. Create the Template file make the template to create the folders of the projects just by running the Python Script file
2. Create a logging template D:\mlops\Crypto_Guardian\src\Crypto\__init__.py here to call the logger 
3. write ur config.yaml file
4. add the paths with the variable to the constants/__init__.py to store the .yaml file paths
5. Write the helper.py file and make the helper function
   

## Plan Of Action
### DAATA Ingestion Plan
1. just write the ETL pipeline 
2. train the model on other dataset(static) from Kaggle
3. save the data into the database (sqlite3)
4. load the data from the database and chanege it to the CSV  file and then do the transformation ,validatinon etc...


# Some thing imp

1. add the @dataclass to the entity/config_entity.py
2. configuration ko dalo config/configuration.py
3. components ko dalo components/ data_ingestion_component.py me 
4. Create the Pipeline/ and then creaate hte pipeline
5. Update the Main.py file
