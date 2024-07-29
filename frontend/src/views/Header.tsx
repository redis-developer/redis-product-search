import { BASE_URL, EMAIL } from "../config";
import Tooltip from '@mui/material/Tooltip';
import '../styles/Header.css';

/* eslint-disable jsx-a11y/anchor-is-valid */
export const Header = () => {
  return (
    <header>
      <div className="header">
        <img
          src={BASE_URL + `/data/redis-logo.png`}
          alt="Redis Logo"
          className="header-logo">
        </img>
        <div className="cta-nav">
          <a href='https://x.com/Redisinc'>
            <Tooltip title="Redis twitter" arrow>
              <img
                alt="x logo"
                src={"/x-logo.svg"}
                className="header-icon-link"
              ></img>
            </Tooltip>
          </a>
          <a href='https://github.com/redis-developer/redis-product-search'>
            <Tooltip title="Project source" arrow>
              <img
                alt="Github logo"
                src="/github-mark-white.svg"
                className="header-icon-link"
              ></img>
            </Tooltip>
          </a>
          <Tooltip title={`${EMAIL}`} arrow>
            <a className="header-cta" href={`mailto:${EMAIL}`}>
              Talk with us!
            </a>
          </Tooltip>
        </div>
      </div>
    </header>
  );
};
