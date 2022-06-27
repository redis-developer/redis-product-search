import * as React from 'react';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';

interface Props {
    gender: string,
    category: string,
    setGender: (state: any) => void;
    setCategory: (state: any) => void;
}

export const TagRadios = (props: Props) => {

  const setProductGender = (event: any) => {
    if (event.target.value === props.gender) {
      props.setGender("");
    } else {
      props.setGender(event.target.value);
    }
  }
  const setProductCategory = (event: any) =>{
    if (event.target.value === props.category) {
      props.setCategory("");
    } else {
      props.setCategory(event.target.value);
    }
  }

  return (
    <FormControl>
      <b>Hybrid Search Attributes</b>
      <div style={{ paddingLeft: "10px", display: "flex", paddingTop: "5% ", gap: "40px"}}>
        <div>
        <FormLabel style={{paddingBottom: "1%"}} id="demo-row-radio-buttons-group-label">Gender</FormLabel>
        <RadioGroup
          value={props.gender}
          aria-labelledby="demo-row-radio-buttons-group-label"
          name="row-radio-buttons-group"
        >
          <FormControlLabel value="Women" control={<Radio size="small" onClick={setProductGender}/>} label="Women" />
          <FormControlLabel value="Men" control={<Radio size="small" onClick={setProductGender}/>} label="Men" />
        </RadioGroup>
        </div>
        <div>
        <FormLabel style={{paddingBottom: "1%"}} id="demo-row-radio-buttons-group-label">Category</FormLabel>
        <RadioGroup
          value={props.category}
          aria-labelledby="demo-row-radio-buttons-group-label"
          name="row-radio-buttons-group"
          >
          <FormControlLabel value="Apparel" control={<Radio size="small" onClick={setProductCategory}/>} label="Apparel" />
          <FormControlLabel value="Accessories" control={<Radio size="small" onClick={setProductCategory} />} label="Accessories" />
          <FormControlLabel value="Footwear" control={<Radio  size="small" onClick={setProductCategory}/>} label="Footwear" />
        </RadioGroup>
        </div>
      </div>
    </FormControl>
  );
}