import React, { useState } from 'react';
//import { makeStyles } from '@material-ui/core/styles';
import { getProducts } from '../api';
import { isAuthenticated } from '../auth';
import { useNavigate } from 'react-router-dom';
import { BASE_URL } from '../config';
import { Card } from "./Card"
import { TagRadios } from '../radio';

/* eslint-disable jsx-a11y/anchor-is-valid */
/* eslint-disable @typescript-eslint/no-unused-vars */

interface Props {
  products: any[];
  setProducts: (state: any) => void;
}


export const Home = (props: Props) => {
  const [error, setError] = useState<string>('');
  const [skip, setSkip] = useState(0);
  const [limit, setLimit] = useState(15);
  const [gender, setGender] = useState<string>('');
  const [category, setCategory] = useState<string>('');
  const Navigate = useNavigate();

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
      { isAuthenticated() ? (
        <p>
        <a className="btn btn-primary m-2" onClick={() => queryProductsWithLimit()}>
         Load Products
        </a>
        <a className="btn btn-secondary m-2" onClick={() => queryProductsWithLimit()}>
         More Products
        </a>
       </p>
      ) : (
        <p>
          <a className="btn btn-primary m-2" onClick={() => Navigate("/login")}>
            Login
          </a>
          <a className="btn btn-secondary m-2" onClick={() => Navigate("/signup")}>
            Sign Up
          </a>
        </p>
      )}
      <TagRadios gender={gender} category={category} setGender={setGender} setCategory={setCategory} />

      </div>
     </section>

      <div className="album py-5 bg-light">
        <div className="container">
          {props.products && (
            <div className="row">

              {props.products.map((product) => (
                <Card
                  key={product.pk}
                  image_path={`${BASE_URL}/data/images/${product.product_id}.jpg`}
                  name={product.product_metadata.name}
                  productId={product.product_id}
                  numProducts={15}
                  gender={gender}
                  category={category}
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