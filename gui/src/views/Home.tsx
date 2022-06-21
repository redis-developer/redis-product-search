import React, { FC, useState } from 'react';
//import { makeStyles } from '@material-ui/core/styles';
import { getProducts } from '../api';
import { BASE_URL } from '../config';
import { Card } from "./Card"

/* eslint-disable jsx-a11y/anchor-is-valid */
/* eslint-disable @typescript-eslint/no-unused-vars */

interface Props {
  products: any[];
  setProducts: (state: any) => void;
}


export const Home = (props: Props) => {
  const [error, setError] = useState<string>('');
  const [skip, setSkip] = useState(0);
  const [limit, setLimit] = useState(10);

  const queryProducts = async () => {
    try {
      const productJson = await getProducts(limit, skip);
      props.setProducts(productJson)
    } catch (err) {
      setError(String(err));
    }
  };

  const queryProductsWithLimit = async () => {
    try {
      setSkip(skip + limit);
      queryProducts();
    } catch (err) {
      console.log(err);
    };
  };


  return (
    <>
      <main role="main">
      <section className="jumbotron text-center mb-0 bg-white" style={{ paddingTop: '40px'}}>
      <div className="container">
       <h1 className="jumbotron-heading">Fashion Product Finder</h1>
       <p className="lead text-muted">
           This demo uses the built in Vector Search capabilities of Redis Enterprise
           show how unstructured data, such as images and text, can be used to create powerful
           search engines.
       </p>
       <p>
        <a href="#" className="btn btn-primary m-2" onClick={() => queryProductsWithLimit()}>
         Load Products
        </a>
        <a href="#" className="btn btn-secondary m-2" onClick={() => queryProductsWithLimit()}>
         More Products
        </a>
       </p>
      </div>
     </section>

      <div className="album py-5 bg-light">
        <div className="container">
          {props.products && (
            <div className="row">

              {props.products.map((product) => (
                  <Card
                  image_path={`${BASE_URL}/data/images/${product.product_id}.jpg`}
                  name={product.product_metadata.name}
                  productId={product.product_id}
                  numProducts={10}
                  setState={props.setProducts}
                  />

                ))}
              </div>
            )}
          </div>
      </div>
      </main>
        </>
  );
};



// <h1>Products</h1>
// {!error && (
//   <a className={classes.link} href="#" onClick={() => queryProducts()}>
//     Load New Products
//   </a>
// )}
//   <div className={classes.gallery}>
//   {products && (
//     <ul>
//       {products.map((product) => (
//           //<p key={product.product_pk}>{product.product_metadata.name}</p>
//           <img className={classes.image} src={`${BASE_URL}/static/images/${product.product_id}.jpg`} alt={product.product_metadata.name}/>
//         ))}
//     </ul>
//     )}
//   </div>
// {error && (
//   <p>
//     Error: <code>{error}</code>
//   </p>
// )}
//   </>
