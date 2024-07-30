/* eslint-disable jsx-a11y/anchor-is-valid */
import { getVisuallySimilarProducts, getSemanticallySimilarProducts } from "../api"
import useCheckMobileScreen from "../mobile"
import Chip from '@mui/material/Chip';
import Tooltip from '@mui/material/Tooltip';

interface Props {
  productId: number;
  numProducts: number;
  imageUrl: string;
  name: string;
  gender: string;
  category: string;
  similarityScore: number;
  setProducts: (state: any) => void;
  setTotal: (state: any) => void;
}


export const Card = (props: Props) => {

  // console.log(props);

  const isMobile = useCheckMobileScreen();

  const queryVisuallySimilarProducts = async () => {
    try {
      const res = await getVisuallySimilarProducts(
        props.productId,
        "KNN",
        props.gender,
        props.category,
        props.numProducts);
      props.setProducts(res.products)
      props.setTotal(res.total)
    } catch (err) {
      console.log(String(err));
    }
  };

  const querySemanticallySimilarProducts = async () => {
    try {
      const res = await getSemanticallySimilarProducts(
        props.productId,
        "KNN",
        props.gender,
        props.category,
        props.numProducts);
      props.setProducts(res.products)
      props.setTotal(res.total)
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
    <div className="col-md-2" style={{ width: getCardSize() }}>
      <div className="card mb-2 box-shadow" style={{ alignContent: 'center' }}>
        <img
          className="card-img-top"
          style={{ height: '60%', width: '60%', alignSelf: 'center' }}
          src={props.imageUrl}
          alt={props.name}
        />
        <div className="card-body">
          <p className="card-text">
            {props.name}
          </p>
          <div style={{ alignContent: "left" }}>
            <b>View Similar:</b>
          </div>
          <div className="d-flex justify-content-between align-items-center">
            <div className="btn-group">
              <Tooltip title="Search for similar products by text" arrow>
                <button
                  type="button"
                  className="btn btn-sm btn-outline-secondary"
                  onClick={() => querySemanticallySimilarProducts()}
                  style={{ fontSize: 12 }}
                >
                  By Text
                </button>
              </Tooltip>
              <Tooltip title="Search for similar products by image" arrow>
                <button
                  type="button"
                  className="btn btn-sm btn-outline-secondary"
                  onClick={() => queryVisuallySimilarProducts()}
                  style={{ fontSize: 12 }}
                >
                  By Image
                </button>
              </Tooltip>
            </div>
            <div className="btn-group">
              {props.similarityScore ? (
                <Tooltip title="Similarity Score" arrow>
                  <Chip
                    style={{ margin: "auto", fontSize: 12 }}
                    label={props.similarityScore.toFixed(2)}
                    color='primary'
                  />
                </Tooltip>
              ) : (
                <></>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

