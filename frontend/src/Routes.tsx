import { FC } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Layout from './Layout';
import { Admin } from './admin';
// import { Login } from './views/Login';
// import { SignUp } from './views/SignUp';

export const AppRoutes: FC = () => {

  return (
    <Router>
      <Routes>
        <Route path="/admin/*" element={<Admin />} />
      </Routes>
      <Routes>
        <Route path="/" element={<Layout />} />
        {/* <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<SignUp />} /> */}
      </Routes>
    </Router>
  );
};
