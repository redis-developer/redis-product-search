import { getProducts } from './api';

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

let skip = 0;
const limit = 15;

export const queryProducts = async (props: Props, gender: string, category: string) => {
  try {
      const result = await getProducts(limit, skip, gender, category);
      props.setProducts(result.products)
      props.setTotal(result.total)
  } catch (err) {
      console.log(err);
  }
};

export const queryProductsWithLimit = async (props: Props) => {
  try {
      skip = skip + limit;
      queryProducts(props, props.gender, props.category);
  } catch (err) {
      console.log(err);
  };
};