import avro.schema

teste_avro = avro({"namespace": "job.avro",
 "type": "record",
 "name": "Job",
 "fields": [
     {"name": "id", "type": "int"},
     {"name": "job",  "type": "string"}
           ]
})

schema = avro.schema.parse(open(teste_avro, "r").read())
print (schema)
