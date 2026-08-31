# Demo login matrix

**Development / demo only.** Change all of these passwords before any production deployment.

## Passwords

| Role | Password |
| --- | --- |
| SUPER_ADMIN | `Admin@12345` |
| TAHSILDAR | `Tahsildar@123` |
| TALUKA_USER | `User@12345` |

## Super Admin

| Username | Role | Taluka |
| --- | --- | --- |
| admin | SUPER_ADMIN | ALL (`taluka = null`) |

Email: `admin@nanded.local`

## Tahsildars

| Username | Role | Taluka |
| --- | --- | --- |
| ardhapur.tahsildar | TAHSILDAR | Ardhapur |
| bhokar.tahsildar | TAHSILDAR | Bhokar |
| biloli.tahsildar | TAHSILDAR | Biloli |
| degloor.tahsildar | TAHSILDAR | Degloor |
| dharmabad.tahsildar | TAHSILDAR | Dharmabad |
| hadgaon.tahsildar | TAHSILDAR | Hadgaon |
| himayatnagar.tahsildar | TAHSILDAR | Himayatnagar |
| kandhar.tahsildar | TAHSILDAR | Kandhar |
| kinwat.tahsildar | TAHSILDAR | Kinwat |
| loha.tahsildar | TAHSILDAR | Loha |
| mahoor.tahsildar | TAHSILDAR | Mahoor |
| mudkhed.tahsildar | TAHSILDAR | Mudkhed |
| mukhed.tahsildar | TAHSILDAR | Mukhed |
| naigaon.tahsildar | TAHSILDAR | Naigaon |
| nanded.tahsildar | TAHSILDAR | Nanded |
| umri.tahsildar | TAHSILDAR | Umri |

## Taluka users (3 per taluka)

| Username | Role | Taluka |
| --- | --- | --- |
| ardhapur.user1 / user2 / user3 | TALUKA_USER | Ardhapur |
| bhokar.user1 / user2 / user3 | TALUKA_USER | Bhokar |
| biloli.user1 / user2 / user3 | TALUKA_USER | Biloli |
| degloor.user1 / user2 / user3 | TALUKA_USER | Degloor |
| dharmabad.user1 / user2 / user3 | TALUKA_USER | Dharmabad |
| hadgaon.user1 / user2 / user3 | TALUKA_USER | Hadgaon |
| himayatnagar.user1 / user2 / user3 | TALUKA_USER | Himayatnagar |
| kandhar.user1 / user2 / user3 | TALUKA_USER | Kandhar |
| kinwat.user1 / user2 / user3 | TALUKA_USER | Kinwat |
| loha.user1 / user2 / user3 | TALUKA_USER | Loha |
| mahoor.user1 / user2 / user3 | TALUKA_USER | Mahoor |
| mudkhed.user1 / user2 / user3 | TALUKA_USER | Mudkhed |
| mukhed.user1 / user2 / user3 | TALUKA_USER | Mukhed |
| naigaon.user1 / user2 / user3 | TALUKA_USER | Naigaon |
| nanded.user1 / user2 / user3 | TALUKA_USER | Nanded |
| umri.user1 / user2 / user3 | TALUKA_USER | Umri |

## Sample records (Hadgaon)

```text
Hadgaon
│
├── hadgaon.tahsildar
│
├── hadgaon.user1
├── hadgaon.user2
├── hadgaon.user3
│
├── HAD-001
├── HAD-002
├── HAD-003
├── HAD-004
└── HAD-005
```

Each taluka has five records named `{Taluka} Record 001` … `005` with codes `{CODE}-001` … `{CODE}-005`.
