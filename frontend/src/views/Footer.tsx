/* eslint-disable jsx-a11y/anchor-is-valid */
import { EMAIL } from '../config'
import '../styles/Footer.css';

export const Footer = () => {
    return (
        <footer>
            <div className='footer'>
                <div>
                    All Redis software used in this demo is licensed according to the  <a href="https://redis.io/docs/stack/license/" > Redis Stack License. </a>
                </div>
                <div>
                    <a href="https://github.com/redis-developer/redis-ai-resources">
                        Redis AI Resources
                    </a>

                    <span> | </span>

                    <a href='https://github.com/redis/redis-vl-python'>
                        RedisVL
                    </a>

                    <span> | </span>

                    <a href='https://redis.io/docs/latest/develop/get-started/vector-database/'>
                        Vector Search Docs
                    </a>
                </div>
                <div>contact: {EMAIL}</div>
            </div>
        </footer>
    );
};