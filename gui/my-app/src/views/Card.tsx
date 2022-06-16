/* eslint-disable jsx-a11y/anchor-is-valid */
import React from 'react';
import { getSimilarProducts } from "../api"


interface Props {
    productId: number;
    numProducts: number;
    image_path: string;
    name: string;
    setState: (state: any) => void;
}


export const Card = (props: Props) => {

    const querySimilarProducts = async () => {
        try {
          const productJson = await getSimilarProducts(
              props.productId,
              "KNN",
              props.numProducts);
          props.setState(productJson)
        } catch (err) {
          console.log(String(err));
        }
      };


    return (
     <div className="col-md-2" style={{width: '20%'}}>
      <div className="card mb-2 box-shadow">
       <img
        className="card-img-top"
        style={{height: '50%', width: '50%', alignSelf: 'center'}}
        src={props.image_path}
        alt={props.name}
       />
       <div className="card-body">
        <p className="card-text">
            {props.name}
        </p>
        <div className="d-flex justify-content-between align-items-center">
         <div className="btn-group">
          <button
           type="button"
           className="btn btn-sm btn-outline-secondary"
           onClick={() => querySimilarProducts()}
          >
           View Similar
          </button>
         </div>
        </div>
       </div>
      </div>
     </div>
    );
   };