# JavaScript Frameworks

One of the lead devs writing these docs made a presentation about this
[here](https://gitlab.com/spwoodcock/presentations/-/tree/main/2024?ref_type=heads)

## Recommendations Summary

- **Simple CRUD app**: use HTMX.
- **Reactive UI & collaborative**: local-first + compiler-based framework.
  - This is mostly where HOTs tools fall.
- **Web business** or complex reactive app: SvelteKit or similar.
- **Organisation-wide consistent UI**: cross-framework _web components_.

### Local-First

- Detailed info [here](https://localfirstweb.dev/)
- In summary, this is possibly the future of web development.
- Instead of managing state on the frontend, we host a database
  entirely in the frontend using WASM.
- This database is synced to the centralised database server.
- Benefits:
  - Realtime Sync: enables real-time synchronization between client-side
    WASM databases and server-side databases.
  - Conflict Resolution: provides mechanisms for handling conflicts and
    ensuring data consistency across distributed systems.
  - Offline Support: allows applications to function offline by maintaining
    local state and syncing changes once back online.

### Backend or Frontend?

There are two crucial questions you should ask before deciding on the
approach to web development taken:

- Does your team skillset lie more in backend or frontend?
- Do you need to optimise for low resource usage on end-user devices,
  or for low connectivity?

Depends on the answer, you may reach for either of the options below.

Hypermedia-based: backend-dev solution | optimise backend:

- Server-centric – minimise frontend.
- Costs more money to run (servers).
- Not as fast as possible local-first solutions.
- But as stated, could have benefits when serving to low-spec devices.
- Small bundle size – less code to transfer.

Frontend (local-first, WASM): frontend-dev solution | optimise frontend:

- Client-centric – minimise backend.
- Cheaper to run.
- May require heavy resource usage on the client: low-spec devices may
  struggle.
- Larger bundle size – more code to transfer.
