import React, { useState } from 'react';
import { Navbar, Container, NavDropdown, Nav, Form, FormControl, Button } from 'react-bootstrap';
import { getProductsByText } from "../api"
import { BASE_URL } from "../config"

interface Props {
  products: any[];
  setProducts: (state: any) => void;
}


/* eslint-disable jsx-a11y/anchor-is-valid */
export const Header = (props: Props) => {
  const [searchText, setText] = useState("");

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


  return (
   <header>
    <Navbar expand="lg" bg="dark" variant="dark" style={{ padding: '25px'}} >
      <Container fluid>

        <Navbar.Brand style={{marginRight: "-30rem"}} href="#">
            <img
              src={BASE_URL + `/static/redis-logo.png`}
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
            style={{ maxHeight: '100px'}}
            navbarScroll
          >
            <Nav.Link href="#action1">Home</Nav.Link>
            <NavDropdown title="About" id="navbarScrollingDropdown">
              <NavDropdown.Item href="#action3">Code</NavDropdown.Item>
              <NavDropdown.Item href="#action4">Blog</NavDropdown.Item>
              <NavDropdown.Divider />
              <NavDropdown.Item href="#action5">
                Redis Vector Search
              </NavDropdown.Item>
            </NavDropdown>
          </Nav>
          <Form className="d-flex">

            <FormControl
              onChange={inputHandler}
              type="search"
              placeholder="Search"
              className="me-2"
              aria-label="Search"
            />
            <Button onClick={() => queryProductsByText()} variant="outline-success">Search</Button>
          </Form>
        </Navbar.Collapse>
      </Container>
    </Navbar>
   </header>
  );
 };