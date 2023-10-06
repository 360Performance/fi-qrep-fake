# DB Test
Docker DB2 Image:
https://www.ibm.com/docs/en/db2/11.5?topic=linux-testing-your-db2-community-edition-docker-image-installation-systems

Daten im Ordner `testdb`, config in `.env_list`

Run via:
```
docker run -h db2server --name db2server --restart=always --detach --privileged=true -p 50000:50000 --env-file .env_list -v ./data:/database ibmcom/db2
```

`db2` utility im contaier als user `db2inst1`.

Connection übernehmen aus Terminal-Server Plugin mit Jar file aus generic execution Plugin (`db2jcc4.jar`).  
Ggf infos aus `java-jdbc-connector-1.2.0.jar` übernehmen.

Querries als .sql files da sehr lang.
