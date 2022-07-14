import React, { FC, useState } from 'react';

import { Header } from './views/Header';
import { Home } from './views/Home';
import { Footer } from './views/Footer';


export const Layout: FC = () => {
    const [products, setProducts] = useState<any[]>([]);
    const [gender, setGender] = useState<string>('');
    const [category, setCategory] = useState<string>('');

    return (
        <>
        <Header setProducts={setProducts} products={products} gender={gender} category={category} setGender={setGender} setCategory={setCategory} />
        <Home setProducts={setProducts} products={products} gender={gender} category={category} setGender={setGender} setCategory={setCategory}/>
        <Footer/>
        </>
    );
};

export default Layout;