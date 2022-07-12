
# Data

The application uses a static dataset of products from Kaggle. There are two
versions that can be used for the demo

 - [Small](https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-dataset) (~.5 GB)
 - [Large](https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-small) (~25 GB)


The small dataset is currently used so that the container remains small but the process is similar for the
larger dataset. The hosted version will use the high-resolution dataset at some point.


### Product Metadata

The file ``styles.csv`` contains the product metadata needed for the demo.

Columns and datatypes of the metadata are listed below.
```text
Int64Index: 44077 entries, 0 to 44423
Data columns (total 10 columns):
 #   Column              Non-Null Count  Dtype
---  ------              --------------  -----
 0   id                  44077 non-null  int64
 1   gender              44077 non-null  object
 2   masterCategory      44077 non-null  object
 3   subCategory         44077 non-null  object
 4   articleType         44077 non-null  object
 5   baseColour          44077 non-null  object
 6   season              44077 non-null  object
 7   year                44077 non-null  int64
 8   usage               44077 non-null  object
 9   productDisplayName  44077 non-null  object
dtypes: int64(2), object(8)
memory usage: 3.7+ MB
```

### Product Images

The images extracted from the archive should



