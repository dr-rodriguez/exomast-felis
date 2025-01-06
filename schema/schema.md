<!--

erDiagram
exomast_Sources {
 BIGINT id PK
   TIMESTAMP modification_date 
   VARCHAR(100) primary_name 
   VARCHAR(30) source_type 
   VARCHAR(30) survey 
}
exomast_Matches {
 BIGINT id1 PK
   BIGINT id2 PK
}
exomast_Names {
 BIGINT id PK
   VARCHAR(100) name PK
}
exomast_Coords {
 BIGINT id PK
   DOUBLE dec 
   DOUBLE ra 
}
exomast_PlanetProperties {
 BIGINT id PK
   FLOAT orbital_period 
   FLOAT orbital_period_error 
   BIGINT orbital_period_ref 
   BIGINT tess_id 
}
exomast_Publications {
 BIGINT id PK
   VARCHAR(30) bibcode 
   VARCHAR(100) reference 
}
exomast_Sources one or zero--1 exomast_Matches : has
exomast_Sources one or zero--1 exomast_Matches : has
exomast_Sources 1--0+ exomast_Names : has
exomast_Sources one or zero--1 exomast_Coords : has
exomast_Sources one or zero--1 exomast_PlanetProperties : has
exomast_Publications one or zero--0+ exomast_PlanetProperties : has

-->
![](https://mermaid.ink/img/ZXJEaWFncmFtCmV4b21hc3RfU291cmNlcyB7CiBCSUdJTlQgaWQgUEsKICAgVElNRVNUQU1QIG1vZGlmaWNhdGlvbl9kYXRlIAogICBWQVJDSEFSKDEwMCkgcHJpbWFyeV9uYW1lIAogICBWQVJDSEFSKDMwKSBzb3VyY2VfdHlwZSAKICAgVkFSQ0hBUigzMCkgc3VydmV5IAp9CmV4b21hc3RfTWF0Y2hlcyB7CiBCSUdJTlQgaWQxIFBLCiAgIEJJR0lOVCBpZDIgUEsKfQpleG9tYXN0X05hbWVzIHsKIEJJR0lOVCBpZCBQSwogICBWQVJDSEFSKDEwMCkgbmFtZSBQSwp9CmV4b21hc3RfQ29vcmRzIHsKIEJJR0lOVCBpZCBQSwogICBET1VCTEUgZGVjIAogICBET1VCTEUgcmEgCn0KZXhvbWFzdF9QbGFuZXRQcm9wZXJ0aWVzIHsKIEJJR0lOVCBpZCBQSwogICBGTE9BVCBvcmJpdGFsX3BlcmlvZCAKICAgRkxPQVQgb3JiaXRhbF9wZXJpb2RfZXJyb3IgCiAgIEJJR0lOVCBvcmJpdGFsX3BlcmlvZF9yZWYgCiAgIEJJR0lOVCB0ZXNzX2lkIAp9CmV4b21hc3RfUHVibGljYXRpb25zIHsKIEJJR0lOVCBpZCBQSwogICBWQVJDSEFSKDMwKSBiaWJjb2RlIAogICBWQVJDSEFSKDEwMCkgcmVmZXJlbmNlIAp9CmV4b21hc3RfU291cmNlcyBvbmUgb3IgemVyby0tMSBleG9tYXN0X01hdGNoZXMgOiBoYXMKZXhvbWFzdF9Tb3VyY2VzIG9uZSBvciB6ZXJvLS0xIGV4b21hc3RfTWF0Y2hlcyA6IGhhcwpleG9tYXN0X1NvdXJjZXMgMS0tMCsgZXhvbWFzdF9OYW1lcyA6IGhhcwpleG9tYXN0X1NvdXJjZXMgb25lIG9yIHplcm8tLTEgZXhvbWFzdF9Db29yZHMgOiBoYXMKZXhvbWFzdF9Tb3VyY2VzIG9uZSBvciB6ZXJvLS0xIGV4b21hc3RfUGxhbmV0UHJvcGVydGllcyA6IGhhcwpleG9tYXN0X1B1YmxpY2F0aW9ucyBvbmUgb3IgemVyby0tMCsgZXhvbWFzdF9QbGFuZXRQcm9wZXJ0aWVzIDogaGFz)
