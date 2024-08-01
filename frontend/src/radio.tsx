import * as React from 'react';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';
import Popover from '@mui/material/Popover';
import Typography from '@mui/material/Typography';
import Tooltip from '@mui/material/Tooltip';
import { queryProducts } from './query';

interface Props {
  products: any[];
  setProducts: (state: any) => void;
  gender: string;
  setGender: (state: any) => void;
  category: string;
  setCategory: (state: any) => void;
  total: number;
  setTotal: (state: any) => void;
}


export const TagRadios = (props: Props) => {
  const [anchorEl, setAnchorEl] = React.useState<HTMLButtonElement | null>(null);

  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const open = Boolean(anchorEl);
  const id = open ? 'simple-popover' : undefined;

  const setProductGender = (event: any) => {
    if (event.target.value === props.gender) {
      props.setGender("");
    } else {
      props.setGender(event.target.value);
      queryProducts(props, event.target.value, props.category)
    }
  }
  const setProductCategory = (event: any) => {
    if (event.target.value === props.category) {
      props.setCategory("");
    } else {
      props.setCategory(event.target.value);
      queryProducts(props, props.gender, event.target.value)
    }
  }
  return (
    <FormControl>
      <div>
        <Tooltip title="Select product tags to use as filters" arrow>
          <button className="btn btn-secondary m-2" onClick={(e) => handleClick(e)}>
            Apply Filters
          </button>
        </Tooltip>
      </div>
      <Popover
        id={id}
        open={open}
        anchorEl={anchorEl}
        onClose={handleClose}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'left',
        }}
      >
        <div style={{ paddingTop: "10px" }}>
          <Typography sx={{ p: 2 }}>
            Hybrid Search combines product filters with vector similarity search.
          </Typography>
          <div style={{ paddingLeft: "10px", display: "flex", paddingTop: "5% ", gap: "30px" }}>
            <div>
              <FormLabel className="radio-label-1" id="demo-row-radio-buttons-group-label">Gender</FormLabel>
              <RadioGroup
                value={props.gender}
                aria-labelledby="demo-row-radio-buttons-group-label"
                name="row-radio-buttons-group"
              >
                <FormControlLabel value="Women" control={<Radio size="small" onClick={setProductGender} />} label="Women" />
                <FormControlLabel value="Men" control={<Radio size="small" onClick={setProductGender} />} label="Men" />
              </RadioGroup>
            </div>
            <div>
              <FormLabel className="radio-label-2" id="demo-row-radio-buttons-group-label">Category</FormLabel>
              <RadioGroup
                value={props.category}
                aria-labelledby="demo-row-radio-buttons-group-label"
                name="row-radio-buttons-group"
              >
                <FormControlLabel value="Apparel" control={<Radio size="small" onClick={setProductCategory} />} label="Apparel" />
                <FormControlLabel value="Accessories" control={<Radio size="small" onClick={setProductCategory} />} label="Accessories" />
                <FormControlLabel value="Footwear" control={<Radio size="small" onClick={setProductCategory} />} label="Footwear" />
              </RadioGroup>
            </div>
          </div>
        </div>
      </Popover>
    </FormControl>
  );
}