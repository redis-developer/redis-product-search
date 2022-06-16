import React, { FC } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Layout from './Layout';


export const AppRoutes: FC = () => {

  return (
        <Router>
            <Routes>
              <Route path="/" element={<Layout/>}/>
            </Routes>
        </Router>
  );
};
