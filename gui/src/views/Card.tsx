/* eslint-disable jsx-a11y/anchor-is-valid */
import React from 'react';
import { getVisuallySimilarProducts, getSemanticallySimilarProducts } from "../api"
import  useCheckMobileScreen  from "../mobile"



interface Props {
    productId: number;
    numProducts: number;
    image_path: string;
    name: string;
    gender: string;
    category: string;
    setState: (state: any) => void;
}


export const Card = (props: Props) => {

    const isMobile = useCheckMobileScreen();

    const queryVisuallySimilarProducts = async () => {
        try {
          const productJson = await getVisuallySimilarProducts(
              props.productId,
              "KNN",
              props.gender,
              props.category,
              props.numProducts);
          props.setState(productJson)
        } catch (err) {
          console.log(String(err));
        }
      };

    const querySemanticallySimilarProducts = async () => {
        try {
          const productJson = await getSemanticallySimilarProducts(
              props.productId,
              "KNN",
              props.gender,
              props.category,
              props.numProducts);
          props.setState(productJson)
        } catch (err) {
          console.log(String(err));
        }
      };


    const getCardSize = () => {
      if (isMobile) {
        return '50%';
      }
      else {
        return '20%';
      }
    }

    return (
     <div className="col-md-2" style={{width: getCardSize()}}>
      <div className="card mb-2 box-shadow" style={{alignContent : 'center'}}>
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
        <div style={{alignContent: "left"}}>
          <b>View Similar:</b>
        </div>
        <div className="d-flex justify-content-between align-items-center">
         <div className="btn-group">
          <button
           type="button"
           className="btn btn-sm btn-outline-secondary"
           onClick={() => querySemanticallySimilarProducts()}
          >
           By Text
          </button>
          <button
           type="button"
           className="btn btn-sm btn-outline-secondary"
           onClick={() => queryVisuallySimilarProducts()}
          >
           By Image
          </button>
         </div>
        </div>
       </div>
      </div>
     </div>
    );
   };