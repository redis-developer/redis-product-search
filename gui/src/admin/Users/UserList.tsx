// in src/users.js
import React, { FC } from 'react';
import {
  List,
  Datagrid,
  TextField,
  BooleanField,
  EmailField,
  EditButton,
} from 'react-admin';

export const UserList: FC = (props) => (
  <List {...props}>
    <Datagrid rowClick="edit">
      <TextField source="pk" />
      <EmailField source="email" />
      <TextField source="first_name" />
      <TextField source="last_name" />
      <TextField source="title" />
      <TextField source="company" />
      <BooleanField source="is_active" />
      <BooleanField source="is_superuser" />
      <EditButton />
    </Datagrid>
  </List>
);
