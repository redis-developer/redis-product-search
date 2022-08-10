import React, { useState } from 'react';
import { Navbar, Container, NavDropdown, Nav, Form, FormControl, Button } from 'react-bootstrap';
import { getProductsByText, getSemanticallySimilarProductsbyText } from "../api"
import { isAuthenticated, logout } from '../auth';
import { BASE_URL } from "../config";
import { useNavigate } from 'react-router-dom';

interface Props {
  products: any[];
  setProducts: (state: any) => void;
  gender: string;
  setGender: (state: any) => void;
  category: string;
  setCategory: (state: any) => void;
}


/* eslint-disable jsx-a11y/anchor-is-valid */
export const Header = (props: Props) => {
  const [searchText, setText] = useState("");
  const Navigate = useNavigate();

   // This function is called when the input changes
   const inputHandler = (event: React.ChangeEvent<HTMLInputElement>) => {
     const enteredText = event.target.value;
     setText(enteredText);
  };

  const queryProductsByText = async () => {
    try {
      const productJson = await getProductsByText(searchText);
      props.setProducts(productJson);
    } catch (err) {
      console.log(String(err));
    }
  };

  const queryProductsByUserText = async () => {
    try {
      const productJson = await getSemanticallySimilarProductsbyText(searchText, props.gender, props.category);
      props.setProducts(productJson);
    } catch (err) {
      console.log(String(err));
    }
  };

  const logoutUser = async () => {
      logout();
      Navigate("/login");
  }

  return (
   <header>
    <Navbar expand="lg" bg="dark" variant="dark" style={{ padding: '25px'}} >
      <Container fluid>
        <Navbar.Brand style={{marginRight: "-30rem"}} href="#">
            <img
              src={BASE_URL + `/data/redis-logo.png`}
              alt="Redis Logo"
              style={{
                height: '7%',
                width: '7%',
                paddingRight: '10px',
                }}>
            </img>
          Redis Vector Search Demo
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="navbarScroll" />
        <Navbar.Collapse id="navbarScroll" style={{top: "5px"}}>
          <Nav
            className="me-auto my-2 my-lg-0"
            style={{ maxHeight: '175px'}}
            navbarScroll
          >
            <NavDropdown title="About" id="navbarScrollingDropdown">
              <NavDropdown.Item href="https://github.com/Spartee/redis-vector-search">Code</NavDropdown.Item>
              <NavDropdown.Item href="http://launchpad.redis.com/">Blog</NavDropdown.Item>
              <NavDropdown.Item href="https://forms.gle/ANpHTe2Da5CVGHty7" target="_blank">Talk With Us</NavDropdown.Item>
              <NavDropdown.Item onClick={() => Navigate("/login")}>Login</NavDropdown.Item>
              <NavDropdown.Item onClick={() => Navigate("/signup")}>Signup</NavDropdown.Item>
              <NavDropdown.Divider />
              <NavDropdown.Item href="https://redis.io/docs/stack/search/reference/vectors/">
                Redis Vector Search
              </NavDropdown.Item>
            </NavDropdown>
          </Nav>
          {/* Add a button to talk with us! */}
          <Nav>
            <Nav.Link className="btn btn-primary m-2" href="https://forms.gle/ANpHTe2Da5CVGHty7" target="_blank">
              Talk With Us
            </Nav.Link>
          </Nav>
          <Form className="d-flex">
            <FormControl
              onChange={inputHandler}
              type="search"
              placeholder="Search"
              onKeyPress={(e) => { e.key === 'Enter' && e.preventDefault(); }}
              className="me-2"
              aria-label="Search"
            />
            <div style={{display: "flex", gap: "3px"}}>
              <Button
              onClick={() => queryProductsByText()}
              variant="outline-success"
              disabled={searchText.length < 1}>
                Search
              </Button>
{/*               <Button
              onClick={() => queryProductsByUserText()}
              variant="outline-success"
              disabled={searchText.length < 1}>
                Vector Search
              </Button>
 */}            </div>
          </Form>
        </Navbar.Collapse>
      </Container>
    </Navbar>
   </header>
  );
 };