# Begraafregisters voor 1811

| License     |                                                                                                                                                 |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Source code | [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)                                     |
| Data        | [![License: CC BY-SA 40](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/40/) |


## Introduction

## Data

Data downloaded from: https://www.amsterdam.nl/stadsarchief/organisatie/open-data/

### Dump
```$ docker exec begraafregisters-voor-1811_db_1 pg_dump -U postgres begraafregisters | gzip > begraafregisters.sql.gz```

### Load
Use a volume mount to load the dump when creating db container: 

```-v path/to/local/begraafregisters.sql.gz:/docker-entrypoint-initdb.d/begraafregisters.sql.gz```

Download dumps: https://surfdrive.surf.nl/files/index.php/s/9cJOMmCOZdLVabp

## Contact

[l.vanwissen@uva.nl](mailto:l.vanwissen@uva.nl)