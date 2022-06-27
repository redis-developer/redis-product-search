import React, { FC, useState } from 'react';
import {
  Paper,
  Grid,
  TextField,
  Button,
  FormControlLabel,
  Checkbox,
} from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import { Face, Fingerprint } from '@mui/icons-material';
import { Alert } from '@mui/material'
import { useNavigate, Navigate } from 'react-router-dom';
import useCheckMobileScreen from '../mobile';
import { login, isAuthenticated } from '../auth';

const useStyles = makeStyles((theme) => ({
  margin: {
    margin: theme.spacing(1),
  },
  padding: {
    padding: theme.spacing(1),
    paddingRight: "10%",
    paddingLeft: "10%"
  },
  button: {
    textTransform: 'none',
  },
  marginTop: {
    marginTop: 10,
  },
}));

export const Login: FC = () => {
  const classes = useStyles();
  const navigate = useNavigate();
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [error, setError] = useState<string>('');

  const handleSubmit = async (_: React.MouseEvent) => {
    setError('');
    try {
      const data = await login(email, password);

      if (data) {
        navigate('/');
      }
    } catch (err) {
      if (err instanceof Error) {
        // handle errors thrown from frontend
        setError(err.message);
      } else {
        // handle errors thrown from master
        setError(String(err));
      }
    }
  };

  const isMobile = useCheckMobileScreen();
  const getSize = () => {
    if (isMobile) {
      return '3%';
    }
    else {
      return '15%';
    }
  }

  return isAuthenticated() ? (
    <Navigate to="/" />
  ) : (
    <div style={{padding: getSize()}}>
    <Paper className={classes.padding}>
      <div className={classes.margin}>
        <Grid container spacing={8} alignItems="flex-end">
          <Grid item>
            <Face />
          </Grid>
          <Grid item md={true} sm={true} xs={true}>
            <TextField
              id="email"
              label="Email"
              type="email"
              value={email}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                setEmail(e.currentTarget.value)
              }
              fullWidth
              autoFocus
              required
            />
          </Grid>
        </Grid>
        <Grid container spacing={8} alignItems="flex-end">
          <Grid item>
            <Fingerprint />
          </Grid>
          <Grid item md={true} sm={true} xs={true}>
            <TextField
              id="password"
              label="Password"
              type="password"
              value={password}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                setPassword(e.currentTarget.value)
              }
              fullWidth
              required
            />
          </Grid>
        </Grid>
        <br />
        <Grid container alignItems="center">
          {error && (
            <Grid item>
              <Alert severity="error">{error}</Alert>
            </Grid>
          )}
        </Grid>
        <Grid container alignItems="center" justifyContent="space-between">
          <Grid item>
            <FormControlLabel
              control={<Checkbox color="primary" />}
              label="Remember me"
            />
          </Grid>
          <Grid item>
            <Button
              disableFocusRipple
              disableRipple
              className={classes.button}
              variant="text"
              color="primary"
            >
              Forgot password ?
            </Button>
          </Grid>
        </Grid>
        <Grid container justifyContent="center" className={classes.marginTop}>
          {' '}
          <Button
            variant="outlined"
            color="primary"
            className={classes.button}
            onClick={() => navigate('/signup')}
          >
            Sign Up
          </Button>{' '}
          &nbsp;
          <Button
            variant="outlined"
            color="primary"
            className={classes.button}
            onClick={handleSubmit}
          >
            Login
          </Button>
        </Grid>
      </div>
    </Paper>
    </div>
  );
};
