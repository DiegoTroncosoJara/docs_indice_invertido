
import axios from 'axios';


export async function searchResults ({search}) {
    if (search === '') return null
    // This should already be declared in your API file
    var app = express();

    // ADD THIS
    var cors = require('cors');
    app.use(cors());
    try {
        console.log("antes del axios y search: ", search);
        // const response = await axios.get("http://0.0.0.0:8000/api/elasticsearch/search?q=Uach")
        // console.log("response: ", response);

        const response = await axios.get('http://0.0.0.0:8000/api/elasticsearch/search', {
            params: {
                q: "Uach"
            }
        });
        console.log("response: ", response);
        
    } catch (error) {
        throw new Error('Error searching results')
    }
}
