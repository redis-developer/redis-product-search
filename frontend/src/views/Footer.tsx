/* eslint-disable jsx-a11y/anchor-is-valid */
import React from 'react';

export const Footer = () => {
    return (
     <footer className="text-muted py-5">
      <div className="container">
      <span>
           All Redis software used in this demo is licensed according to the  <a href="https://redis.io/docs/stack/license/" > Redis Stack License. </a>
        </span>
       <p className="float-right">
        <a href="#">Back to top</a>
       </p>
      </div>
     </footer>
    );
};