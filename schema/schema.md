<!--

erDiagram
exomast_Sources {
 BIGINT id PK
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
}
exomast_Properties {
 BIGINT id PK
   VARCHAR(30) property_type PK
   FLOAT property_error 
   BIGINT property_reference 
   FLOAT property_value 
}
exomast_Publications {
 BIGINT id PK
   VARCHAR(30) ref 
   VARCHAR(100) reference 
}
exomast_Sources one or zero--1 exomast_Matches : has
exomast_Sources one or zero--1 exomast_Matches : has
exomast_Sources 1--0+ exomast_Names : has
exomast_Sources one or zero--1 exomast_Coords : has
exomast_Sources one or zero--1 exomast_PlanetProperties : has
exomast_Publications one or zero--0+ exomast_PlanetProperties : has
exomast_Sources one or zero--0+ exomast_Properties : has
exomast_Publications one or zero--0+ exomast_Properties : has

-->
![](https://mermaid.ink/img/ZXJEaWFncmFtCmV4b21hc3RfU291cmNlcyB7CiBCSUdJTlQgaWQgUEsKICAgVkFSQ0hBUigxMDApIHByaW1hcnlfbmFtZSAKICAgVkFSQ0hBUigzMCkgc291cmNlX3R5cGUgCiAgIFZBUkNIQVIoMzApIHN1cnZleSAKfQpleG9tYXN0X01hdGNoZXMgewogQklHSU5UIGlkMSBQSwogICBCSUdJTlQgaWQyIFBLCn0KZXhvbWFzdF9OYW1lcyB7CiBCSUdJTlQgaWQgUEsKICAgVkFSQ0hBUigxMDApIG5hbWUgUEsKfQpleG9tYXN0X0Nvb3JkcyB7CiBCSUdJTlQgaWQgUEsKICAgRE9VQkxFIGRlYyAKICAgRE9VQkxFIHJhIAp9CmV4b21hc3RfUGxhbmV0UHJvcGVydGllcyB7CiBCSUdJTlQgaWQgUEsKICAgRkxPQVQgb3JiaXRhbF9wZXJpb2QgCiAgIEZMT0FUIG9yYml0YWxfcGVyaW9kX2Vycm9yIAogICBCSUdJTlQgb3JiaXRhbF9wZXJpb2RfcmVmIAp9CmV4b21hc3RfUHJvcGVydGllcyB7CiBCSUdJTlQgaWQgUEsKICAgVkFSQ0hBUigzMCkgcHJvcGVydHlfdHlwZSBQSwogICBGTE9BVCBwcm9wZXJ0eV9lcnJvciAKICAgQklHSU5UIHByb3BlcnR5X3JlZmVyZW5jZSAKICAgRkxPQVQgcHJvcGVydHlfdmFsdWUgCn0KZXhvbWFzdF9QdWJsaWNhdGlvbnMgewogQklHSU5UIGlkIFBLCiAgIFZBUkNIQVIoMzApIHJlZiAKICAgVkFSQ0hBUigxMDApIHJlZmVyZW5jZSAKfQpleG9tYXN0X1NvdXJjZXMgb25lIG9yIHplcm8tLTEgZXhvbWFzdF9NYXRjaGVzIDogaGFzCmV4b21hc3RfU291cmNlcyBvbmUgb3IgemVyby0tMSBleG9tYXN0X01hdGNoZXMgOiBoYXMKZXhvbWFzdF9Tb3VyY2VzIDEtLTArIGV4b21hc3RfTmFtZXMgOiBoYXMKZXhvbWFzdF9Tb3VyY2VzIG9uZSBvciB6ZXJvLS0xIGV4b21hc3RfQ29vcmRzIDogaGFzCmV4b21hc3RfU291cmNlcyBvbmUgb3IgemVyby0tMSBleG9tYXN0X1BsYW5ldFByb3BlcnRpZXMgOiBoYXMKZXhvbWFzdF9QdWJsaWNhdGlvbnMgb25lIG9yIHplcm8tLTArIGV4b21hc3RfUGxhbmV0UHJvcGVydGllcyA6IGhhcwpleG9tYXN0X1NvdXJjZXMgb25lIG9yIHplcm8tLTArIGV4b21hc3RfUHJvcGVydGllcyA6IGhhcwpleG9tYXN0X1B1YmxpY2F0aW9ucyBvbmUgb3IgemVyby0tMCsgZXhvbWFzdF9Qcm9wZXJ0aWVzIDogaGFz)
