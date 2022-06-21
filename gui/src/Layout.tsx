import React, { FC, useState } from 'react';

import { Header } from './views/Header';
import { Home } from './views/Home';
import { Footer } from './views/Footer';


export const Layout: FC = () => {
    const [products, setProducts] = useState<any[]>([]);

    return (
        <>
        <Header setProducts={setProducts} products={products} />
        <Home setProducts={setProducts} products={products}/>
        <Footer/>
        </>
    );
};

export default Layout;