import React from 'react';
import { Modal, Card, Button, Row, Col } from 'react-bootstrap';
import API_CONFIG from '../../../config';
import styles from './MemberDetailsModal.module.css';


const MemberDetailsModal = ({ show, member, onClose }) => {
  if (!show || !member) {
    return null;
  }

  // Function to handle image loading error
  const handleImageError = (event) => {
    event.target.style.display = 'none'; // Hide the image if it fails to load
  };
  // Parse the notes JSON string into an array of objects
  const parsedNotes = JSON.parse(member.notes);

  return (
    <Modal show={show} onHide={onClose} dir="rtl" centered>
      <Modal.Header closeButton className={styles.modalHeader}>
        <Modal.Title className={styles.modalTitle}>تفاصيل العضو</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Card className="mb-3">
          <Card.Body>
            <Row>
              <Col md={6} className="d-flex align-items-center justify-content-center">
                {/* Add member's photo here */}
                <div
                  className={`rounded-circle overflow-hidden mx-auto d-block mb-2 ${styles.photoWrapper}`}
                >
                  {member.photo ? (
                    <Card.Img
                      src={`${API_CONFIG.baseURL}/UserPics/${member.photo}`}
                      alt="Member Photo"
                      className={styles.memberImage}
                      onError={handleImageError}
                    />
                  ) : (
                    <div
                      className="d-flex align-items-center justify-content-center"
                      className={styles.noPhoto}
                    >
                      صورة العضو غير متوفرة
                    </div>
                  )}
                </div>
              </Col>
              <Col md={6}>
                <Card.Title className={styles.cardTitle}>بيانات العضو</Card.Title>
                <Card.Text className={styles.infoText}>الاسم: {member.name}</Card.Text>
                <Card.Text className={styles.infoText}>الرقم التسجيلي: {member.member_id}</Card.Text>
                <Card.Text className={styles.infoText}>الفئة: {member.category_id}</Card.Text>
                <Card.Text className={styles.infoText}>العلاقة: {member.relation_id}</Card.Text>
                <Card.Text className={styles.infoText}>الجنس: {member.gender}</Card.Text>
                <Card.Text className={styles.infoText}>الديانة: {member.relegion}</Card.Text>
                <Card.Text className={styles.infoText}>العنوان: {member.address}</Card.Text>
                <Card.Text className={styles.infoText}>المهنة: {member.profession}</Card.Text>
                <Card.Text className={styles.infoText}>الحالة: {member.status_id}</Card.Text>
                <Card.Text className={styles.infoText}>الهاتف: {member.phone}</Card.Text>
              </Col>
               </Row>
              
<div>
  <h5>Notes:</h5>
  {parsedNotes.length > 0 ? (
    parsedNotes.map((note, index) => (
      <div key={index}>
        {note.note && <p>Created By: {note.createdBy}</p>}
        {note.note && <p>Note: {note.note}</p>}
        {note.note && <p>Created At: {note.createdAt}</p>}
      </div>
    ))
  ) : (
    <p>No notes available for this member.</p>
  )}
</div>

        </Card.Body>
      </Card>
    </Modal.Body>
    <Modal.Footer>
      <Button variant="secondary" onClick={onClose}>
        إغلاق
      </Button>
    </Modal.Footer>
  </Modal>
  );
};

export default MemberDetailsModal;
