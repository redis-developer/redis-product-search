import React, { FC, useState } from 'react';
import { Paper, Grid, TextField, Button } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import { Face, Fingerprint } from '@mui/icons-material';
import { Alert } from '@mui/material';
import { useNavigate, Navigate } from 'react-router-dom';
import useCheckMobileScreen from '../mobile';
import { signUp, isAuthenticated } from '../auth';

const useStyles = makeStyles((theme) => ({
  margin: {
    margin: theme.spacing(2),
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

export const SignUp: FC = () => {
  const classes = useStyles();
  const navigate = useNavigate();
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [passwordConfirmation, setPasswordConfirmation] = useState<string>('');
  const [company, setCompany] = useState<string>('');
  const [first, setFirst] = useState<string>('');
  const [last, setLast] = useState<string>('');
  const [title, setTitle] = useState<string>('');
  const [error, setError] = useState<string>('');

  const handleSubmit = async (_: React.MouseEvent) => {
    // Password confirmation validation
    if (password !== passwordConfirmation) setError('Passwords do not match!');
    else {
      setError('');
      try {
        const data = await signUp(first, last, email, password, passwordConfirmation, company, title);

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
              id="firstname"
              label="First Name"
              type="text"
              value={first}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                setFirst(e.currentTarget.value)
              }
              fullWidth
              autoFocus
              required
            />
          </Grid>
        </Grid>
        <Grid container spacing={8} alignItems="flex-end">
          <Grid item>
            <Face />
          </Grid>
          <Grid item md={true} sm={true} xs={true}>
            <TextField
              id="last"
              label="Last Name"
              type="text"
              value={last}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                setLast(e.currentTarget.value)
              }
              fullWidth
              autoFocus
              required
            />
          </Grid>
        </Grid>
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
            <Face />
          </Grid>
          <Grid item md={true} sm={true} xs={true}>
            <TextField
              id="company"
              label="Company"
              type="company"
              value={company}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                setCompany(e.currentTarget.value)
              }
              fullWidth
              autoFocus
              required
            />
          </Grid>
        </Grid>
        <Grid container spacing={8} alignItems="flex-end">
          <Grid item>
            <Face />
          </Grid>
          <Grid item md={true} sm={true} xs={true}>
            <TextField
              id="title"
              label="Title"
              type="title"
              value={title}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                setTitle(e.currentTarget.value)
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
        <Grid container spacing={8} alignItems="flex-end">
          <Grid item>
            <Fingerprint />
          </Grid>
          <Grid item md={true} sm={true} xs={true}>
            <TextField
              id="passwordConfirmation"
              label="Confirm password"
              type="password"
              value={passwordConfirmation}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                setPasswordConfirmation(e.currentTarget.value)
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
        <Grid container justifyContent="center" className={classes.marginTop}>
          <Button
            variant="outlined"
            color="primary"
            className={classes.button}
            onClick={handleSubmit}
          >
            Sign Up
          </Button>
        </Grid>
      </div>
    </Paper>
    </div>
  );
};
