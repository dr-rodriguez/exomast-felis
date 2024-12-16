<!--

erDiagram
exomast_Sources {
 BIGINT id PK
   VARCHAR(100) name 
   VARCHAR(30) survey 
   VARCHAR(30) type 
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
   VARCHAR(30) property PK
   DOUBLE value 
}
exomast_Sources one or zero--1 exomast_Matches : has
exomast_Sources one or zero--1 exomast_Matches : has
exomast_Sources 1--0+ exomast_Names : has
exomast_Sources one or zero--1 exomast_Coords : has
exomast_Sources one or zero--0+ exomast_PlanetProperties : has

-->
![](https://mermaid.ink/img/ZXJEaWFncmFtCmV4b21hc3RfU291cmNlcyB7CiBCSUdJTlQgaWQgUEsKICAgVkFSQ0hBUigxMDApIG5hbWUgCiAgIFZBUkNIQVIoMzApIHN1cnZleSAKICAgVkFSQ0hBUigzMCkgdHlwZSAKfQpleG9tYXN0X01hdGNoZXMgewogQklHSU5UIGlkMSBQSwogICBCSUdJTlQgaWQyIFBLCn0KZXhvbWFzdF9OYW1lcyB7CiBCSUdJTlQgaWQgUEsKICAgVkFSQ0hBUigxMDApIG5hbWUgUEsKfQpleG9tYXN0X0Nvb3JkcyB7CiBCSUdJTlQgaWQgUEsKICAgRE9VQkxFIGRlYyAKICAgRE9VQkxFIHJhIAp9CmV4b21hc3RfUGxhbmV0UHJvcGVydGllcyB7CiBCSUdJTlQgaWQgUEsKICAgVkFSQ0hBUigzMCkgcHJvcGVydHkgUEsKICAgRE9VQkxFIHZhbHVlIAp9CmV4b21hc3RfU291cmNlcyBvbmUgb3IgemVyby0tMSBleG9tYXN0X01hdGNoZXMgOiBoYXMKZXhvbWFzdF9Tb3VyY2VzIG9uZSBvciB6ZXJvLS0xIGV4b21hc3RfTWF0Y2hlcyA6IGhhcwpleG9tYXN0X1NvdXJjZXMgMS0tMCsgZXhvbWFzdF9OYW1lcyA6IGhhcwpleG9tYXN0X1NvdXJjZXMgb25lIG9yIHplcm8tLTEgZXhvbWFzdF9Db29yZHMgOiBoYXMKZXhvbWFzdF9Tb3VyY2VzIG9uZSBvciB6ZXJvLS0wKyBleG9tYXN0X1BsYW5ldFByb3BlcnRpZXMgOiBoYXM=)
