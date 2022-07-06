import * as React from 'react';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';
import Popover from '@mui/material/Popover';
import Typography from '@mui/material/Typography';
import { makeStyles } from '@material-ui/core/styles';
import useCheckMobileScreen from './mobile';
interface Props {
    gender: string,
    category: string,
    setGender: (state: any) => void;
    setCategory: (state: any) => void;
}


const useStyles = makeStyles((theme) => ({
  popover: {
    padding: theme.spacing(1),
    width: "50%"
  },
  popoverMobile: {
    padding: theme.spacing(1),
    width: "85%"
  }
}));

export const TagRadios = (props: Props) => {
  const [anchorEl, setAnchorEl] = React.useState<HTMLButtonElement | null>(null);
  const classes = useStyles();

  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const open = Boolean(anchorEl);
  const id = open ? 'simple-popover' : undefined;

  const isMobile = useCheckMobileScreen();
  const getPopoverClass = () => {
    if (isMobile) {
      return classes.popoverMobile;
    }
    else {
      return classes.popover;
    }
  }
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
      <div>
        <button className="btn btn-secondary m-2" onClick={(e) => handleClick(e)}>
              Set Hybrid Search Attributes
        </button>
    </div>
    <Popover
      id={id}
      className={getPopoverClass()}
      open={open}
      anchorEl={anchorEl}
      onClose={handleClose}
      anchorOrigin={{
        vertical: 'bottom',
        horizontal: 'left',
      }}
    >
      <div style={{paddingTop: "10px"}}>
        <Typography sx={{ p: 2 }}>
          Hybrid Search combines tag based filtering with vector search.
          Selected tags will pre-filter results found by the text and image vector search.
          </Typography>
      <div style={{ paddingLeft: "10px", display: "flex", paddingTop: "5% ", gap: "30px"}}>
        <div>
        <FormLabel className="radio-label-1" id="demo-row-radio-buttons-group-label">Gender</FormLabel>
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
        <FormLabel className="radio-label-2" id="demo-row-radio-buttons-group-label">Category</FormLabel>
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
      </div>
    </Popover>
    </FormControl>
  );
}