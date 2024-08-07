import { initializeApp } from 'firebase/app';
import { getFirestore, collection, getDocs } from 'firebase/firestore/lite';
import { getAuth, OnAuthStateChanged } from "firebase/auth";



const firebaseConfig = {
    apiKey: "AIzaSyAN9oUD8S4sTBaFJT6yyJbfyZzTPtTHS78",
    authDomain: "gcbp-fe364.firebaseapp.com",
    projectId: "gcbp-fe364",
    storageBucket: "gcbp-fe364.appspot.com",
    messagingSenderId: "615512236165",
    appId: "1:615512236165:web:0611217a3d1deed4e149ec",
    measurementId: "G-L6H2YZDE89"
  };

const app = initializeApp(firebaseConfig);
const db = getFirestore(firebaseApp);
const auth = getAuth(firebaseApp)


