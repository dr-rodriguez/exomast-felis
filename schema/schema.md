<!--

erDiagram
exomast_Sources {
 BIGINT id PK
   VARCHAR(100) name 
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
![](https://mermaid.ink/img/ZXJEaWFncmFtCmV4b21hc3RfU291cmNlcyB7CiBCSUdJTlQgaWQgUEsKICAgVkFSQ0hBUigxMDApIG5hbWUgCiAgIFZBUkNIQVIoMzApIHNvdXJjZV90eXBlIAogICBWQVJDSEFSKDMwKSBzdXJ2ZXkgCn0KZXhvbWFzdF9NYXRjaGVzIHsKIEJJR0lOVCBpZDEgUEsKICAgQklHSU5UIGlkMiBQSwp9CmV4b21hc3RfTmFtZXMgewogQklHSU5UIGlkIFBLCiAgIFZBUkNIQVIoMTAwKSBuYW1lIFBLCn0KZXhvbWFzdF9Db29yZHMgewogQklHSU5UIGlkIFBLCiAgIERPVUJMRSBkZWMgCiAgIERPVUJMRSByYSAKfQpleG9tYXN0X1BsYW5ldFByb3BlcnRpZXMgewogQklHSU5UIGlkIFBLCiAgIEZMT0FUIG9yYml0YWxfcGVyaW9kIAogICBGTE9BVCBvcmJpdGFsX3BlcmlvZF9lcnJvciAKICAgQklHSU5UIG9yYml0YWxfcGVyaW9kX3JlZiAKfQpleG9tYXN0X1Byb3BlcnRpZXMgewogQklHSU5UIGlkIFBLCiAgIFZBUkNIQVIoMzApIHByb3BlcnR5X3R5cGUgUEsKICAgRkxPQVQgcHJvcGVydHlfZXJyb3IgCiAgIEJJR0lOVCBwcm9wZXJ0eV9yZWZlcmVuY2UgCiAgIEZMT0FUIHByb3BlcnR5X3ZhbHVlIAp9CmV4b21hc3RfUHVibGljYXRpb25zIHsKIEJJR0lOVCBpZCBQSwogICBWQVJDSEFSKDMwKSByZWYgCiAgIFZBUkNIQVIoMTAwKSByZWZlcmVuY2UgCn0KZXhvbWFzdF9Tb3VyY2VzIG9uZSBvciB6ZXJvLS0xIGV4b21hc3RfTWF0Y2hlcyA6IGhhcwpleG9tYXN0X1NvdXJjZXMgb25lIG9yIHplcm8tLTEgZXhvbWFzdF9NYXRjaGVzIDogaGFzCmV4b21hc3RfU291cmNlcyAxLS0wKyBleG9tYXN0X05hbWVzIDogaGFzCmV4b21hc3RfU291cmNlcyBvbmUgb3IgemVyby0tMSBleG9tYXN0X0Nvb3JkcyA6IGhhcwpleG9tYXN0X1NvdXJjZXMgb25lIG9yIHplcm8tLTEgZXhvbWFzdF9QbGFuZXRQcm9wZXJ0aWVzIDogaGFzCmV4b21hc3RfUHVibGljYXRpb25zIG9uZSBvciB6ZXJvLS0wKyBleG9tYXN0X1BsYW5ldFByb3BlcnRpZXMgOiBoYXMKZXhvbWFzdF9Tb3VyY2VzIG9uZSBvciB6ZXJvLS0wKyBleG9tYXN0X1Byb3BlcnRpZXMgOiBoYXMKZXhvbWFzdF9QdWJsaWNhdGlvbnMgb25lIG9yIHplcm8tLTArIGV4b21hc3RfUHJvcGVydGllcyA6IGhhcw==)
