## Working with MongoDB

### Task 1 - Import `catalog.json` into mongodb server into a database named `catalog` and a collection named `electronics`
```bash
mongoimport -u root --authenticationDatabase admin --db catalog --collection electronics --file catalog.json
```

### Task 2 - List out all the databases
```bash 
show databases
```

### Task 3 - List out all the collections in the database
```bash 
show collections
```

### Task 4 - Create an index on the field "type"
```bash 
db.eletronics.createIndex({type: 1})
  {
    "createdCollectionAutomatically" : false,
    "numIndexesBefore" : 1,
    "numIndexesAfer": 2,
    "ok" : 1
  }
```
      
### Task 5 - Write a query to find the count of laptops
```bash
db.eletronics.find({"type": "laptop"}).count()
```

### Task 6 - Write a query to find the number of mobile phones with screen size of 6 inches
```bash
db.eletronics.find({"type": "smart phone", "screen size": {$eq: 6}}).count()
```

### Task 7 - Write a query to find out the average screen size of smart phones
```bash
db.eletronics.aggregate([
  {
    $match: "type": "smart phone"
  },
  {
    "$group":{
      "_id": null,
      "average_screen_size":{"$avg": "$screen size"}
    }
  }
])
{"_id" : null, "average_screen_size" : 6}
```

### Task 8 - Export the fields `id`, `type`, `model`, from the **electronics** collection into a file named `electronics.csv`
```bash
mongoexport -u root --authenticationDatabase admin --db catalog --collection electronics --out electronics.csv --type=csv --fields _id,type,model
```
