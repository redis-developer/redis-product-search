import { FC, useState } from 'react';

import { Header } from './views/Header';
import { Home } from './views/Home';
import { Footer } from './views/Footer';


export const Layout: FC = () => {
    const [products, setProducts] = useState<any[]>([]);
    const [gender, setGender] = useState<string>('');
    const [category, setCategory] = useState<string>('');
    const [total, setTotal] = useState<number>(0);

    return (
        <>
            <Header />
            <Home
                products={products}
                setProducts={setProducts}
                gender={gender}
                category={category}
                setCategory={setCategory}
                total={total}
                setTotal={setTotal}
                setGender={setGender}
            />
            <Footer />
        </>
    );
};

export default Layout;