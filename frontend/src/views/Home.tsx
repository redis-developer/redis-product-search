import { useEffect } from 'react';
import { Card } from "./Card"
import { TagRadios } from '../radio';
import Chip from '@mui/material/Chip';
import Tooltip from '@mui/material/Tooltip';
import { queryProducts, queryProductsWithLimit } from '../query';

/* eslint-disable jsx-a11y/anchor-is-valid */
/* eslint-disable @typescript-eslint/no-unused-vars */

interface Props {
  products: any[];
  setProducts: (state: any) => void;
  gender: string;
  setGender: (state: any) => void;
  category: string;
  setCategory: (state: any) => void;
  total: number;
  setTotal: (state: any) => void;
}

export const Home = (props: Props) => {
  // Execute this one when the component loads up
  useEffect(() => {
    // clear filters
    props.setGender("");
    props.setCategory("");
    queryProductsWithLimit(props);
  }, []);

  return (
    <>
      <main role="main">
        <section className="jumbotron text-center mb-0 bg-white" style={{ paddingTop: '40px' }}>
          <div className="container">
            <h1 className="jumbotron-heading">Fashion Product Finder</h1>
            <p className="lead text-muted">
              This demo uses the built in Vector Search capabilities of Redis Enterprise
              to show how unstructured data, such as images and text, can be used to create powerful
              search engines.
            </p>
            <div>
              <div className="btn-group">
                {props.products.length > 0 ? (
                  <div>
                    <TagRadios
                      gender={props.gender}
                      category={props.category}
                      products={props.products}
                      total={props.total}
                      setGender={props.setGender}
                      setCategory={props.setCategory}
                      setProducts={props.setProducts}
                      setTotal={props.setTotal}
                    />
                  </div>
                ) : (
                  <></>
                )}
                <Tooltip title="Fetch more products from Redis" arrow>
                  <a className="btn btn-primary m-2" onClick={() => queryProductsWithLimit(props)}>
                    Load More Products
                  </a>
                </Tooltip>
              </div>
            </div>
          </div>
        </section>
        <div className="album py-5 bg-light">
          <div className="container">
            <p style={{ fontSize: 15 }}>
              <Tooltip title="Filtered product count" arrow>
                <em>{props.total} searchable products</em>
              </Tooltip>
            </p>
            <div>
              {props.category != "" ? (
                <Chip
                  style={{ margin: "5px 5px 25px 5px" }}
                  label={`Category: ${props.category}`}
                  variant='outlined'
                  clickable
                  color='primary'
                  onDelete={() => { props.setCategory(""); queryProducts(props, props.gender, "") }}
                  disabled={props.category == ''}
                />
              ) : (
                <></>
              )}
              {props.gender != "" ? (
                <Chip
                  style={{ margin: "5px 5px 25px 5px" }}
                  label={`Gender: ${props.gender}`}
                  variant='outlined'
                  clickable
                  color='primary'
                  onDelete={() => { props.setGender(""); queryProducts(props, "", props.category) }}
                  disabled={props.gender == ''}
                />
              ) : (
                <></>
              )}
            </div>
            {props.products && (
              <div className="row">

                {props.products.map((product) => (
                  <Card
                    key={product.pk}
                    image_path={product.product_metadata.image_url}
                    name={product.product_metadata.name}
                    productId={product.product_id}
                    numProducts={15}
                    similarity_score={product.similarity_score}
                    gender={props.gender}
                    category={props.category}
                    setProducts={props.setProducts}
                    setTotal={props.setTotal}
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