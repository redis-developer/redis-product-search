import { FC } from 'react';
import { Admin as ReactAdmin, Resource } from 'react-admin';
import authProvider from './authProvider';
import { UserList, UserEdit, UserCreate } from './Users';
import { dataProvider } from './dataProvider';


export const Admin: FC = () => {
  return (
    <ReactAdmin basename="/admin" dataProvider={dataProvider} authProvider={authProvider} >
        <Resource
          name="users"
          list={UserList}
          edit={UserEdit}
          create={UserCreate}
        />
    </ReactAdmin>
  );
};
