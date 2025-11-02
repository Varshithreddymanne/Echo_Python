import { useEffect, useState } from "react";
import { Box, Heading, Button, Flex } from "@chakra-ui/react";
import API from "../api";
import PostCard from "../components/PostCard";
import { Link } from "react-router-dom";

export default function Feed() {
  const [posts, setPosts] = useState([]);

  const load = async () => {
    try{
      const res = await API.get("/posts");
      console.log("reponse: ", res.data);
      setPosts(res.data);
    }catch (err) {
      console.error("Error loading posts:", err);
    }
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <Box p={6}>
      <Flex justify="space-between" align="center">
        <Heading>Echo Feed</Heading>
        <Flex gap={2}>
          <Link to="/create"><Button>Create Post</Button></Link>
          <Link to="/login"><Button>Login</Button></Link>
          <Link to="/register"><Button>Register</Button></Link>
        </Flex>
      </Flex>
      {Array.isArray(posts) && posts.length > 0 ? (
        posts.map((p) => (
        <PostCard key={p._id} post={p} refresh={load} />))) : ( <p>No posts yet.</p>)
      }
    </Box>
  );
}
